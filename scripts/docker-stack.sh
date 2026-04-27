#!/usr/bin/env bash
# One-shot orchestrator: bring the full stack up in Docker, wait for health,
# then run smoke tests against every exposed service.
#
# Usage:
#   scripts/docker-stack.sh up      # build + start + wait healthy + smoke test
#   scripts/docker-stack.sh down    # stop and remove containers (keep volumes)
#   scripts/docker-stack.sh clean   # down + remove named volumes
#   scripts/docker-stack.sh test    # run smoke tests against a running stack
#   scripts/docker-stack.sh seed    # idempotently create demo learner + admin
#   scripts/docker-stack.sh logs    # tail service logs

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; YELLOW=$'\033[1;33m'; DIM=$'\033[2m'; RESET=$'\033[0m'
log()   { printf '%s[stack]%s %s\n' "$DIM" "$RESET" "$*"; }
ok()    { printf '%s[ok]%s    %s\n' "$GREEN" "$RESET" "$*"; }
warn()  { printf '%s[warn]%s  %s\n' "$YELLOW" "$RESET" "$*"; }
fail()  { printf '%s[fail]%s  %s\n' "$RED" "$RESET" "$*" >&2; }

compose() {
  if docker compose version >/dev/null 2>&1; then
    docker compose "$@"
  elif command -v docker-compose >/dev/null 2>&1; then
    docker-compose "$@"
  else
    fail "docker compose is not installed"
    exit 1
  fi
}

ensure_env() {
  if [[ ! -f .env ]]; then
    if [[ -f .env.example ]]; then
      cp .env.example .env
      warn ".env was missing; copied from .env.example (edit secrets before shipping)"
      return
    fi
    fail ".env and .env.example are both missing"
    exit 1
  fi

  # Detect stale .env: every key in .env.example must be present in .env.
  local missing=()
  while IFS='=' read -r key _; do
    [[ -z "$key" || "$key" == \#* ]] && continue
    grep -qE "^${key}=" .env || missing+=("$key")
  done < .env.example
  if (( ${#missing[@]} > 0 )); then
    warn ".env is missing keys from .env.example: ${missing[*]}"
    warn "run:  mv .env .env.backup && cp .env.example .env  (then re-add your secrets)"
  fi
}

wait_healthy() {
  local service=$1 timeout=${2:-180} elapsed=0
  log "waiting for '$service' to become healthy (timeout ${timeout}s)"
  while (( elapsed < timeout )); do
    local cid status
    cid=$(compose ps -q "$service" 2>/dev/null || true)
    if [[ -n "$cid" ]]; then
      status=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' "$cid" 2>/dev/null || echo "unknown")
      case "$status" in
        healthy|running) ok "$service: $status"; return 0 ;;
        unhealthy|exited|dead) fail "$service entered state '$status'"; compose logs --tail=50 "$service" >&2; return 1 ;;
      esac
    fi
    sleep 2; elapsed=$((elapsed+2))
  done
  fail "$service did not become healthy within ${timeout}s"
  compose logs --tail=80 "$service" >&2
  return 1
}

expect_http() {
  local name=$1 url=$2 expect=${3:-200}
  local code
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url" || echo "000")
  if [[ "$code" == "$expect" ]]; then
    ok "$name -> HTTP $code ($url)"
    return 0
  fi
  fail "$name expected HTTP $expect but got $code ($url)"
  return 1
}

smoke_test() {
  local fails=0
  log "running smoke tests..."

  local health_body
  health_body=$(curl -s --max-time 10 http://localhost:8000/api/health || echo "")
  if [[ "$health_body" == *'"status":"ok"'* ]]; then
    ok "backend /api/health -> $health_body"
  else
    fail "backend /api/health did not return ok (got: $health_body)"; fails=$((fails+1))
  fi

  expect_http "backend openapi"  http://localhost:8000/api/openapi.json 200 || fails=$((fails+1))
  expect_http "frontend root"    http://localhost:3000/ 200 || fails=$((fails+1))
  expect_http "minio health"     http://localhost:9000/minio/health/live 200 || fails=$((fails+1))

  local bucket=${MINIO_BUCKET:-$(grep -E '^MINIO_BUCKET=' .env | cut -d= -f2- || echo edulingo-audio)}
  if compose exec -T minio mc --version >/dev/null 2>&1; then :; fi
  local bucket_ok
  bucket_ok=$(compose run --rm -T --entrypoint sh minio-bootstrap -c \
      "mc alias set local http://minio:9000 \"\$MINIO_ACCESS_KEY\" \"\$MINIO_SECRET_KEY\" >/dev/null 2>&1 && mc ls local/${bucket} >/dev/null 2>&1 && echo OK || echo MISS" \
      2>/dev/null | tail -n1 || echo MISS)
  if [[ "$bucket_ok" == "OK" ]]; then
    ok "minio bucket '$bucket' exists"
  else
    fail "minio bucket '$bucket' missing or unreachable"; fails=$((fails+1))
  fi

  if (( fails == 0 )); then
    ok "all smoke tests passed"
    return 0
  fi
  fail "$fails smoke test(s) failed"
  return 1
}

cmd_up() {
  ensure_env
  log "building images and starting stack..."
  compose up -d --build
  log "stack started; polling health..."
  wait_healthy postgres 60
  wait_healthy redis 30
  wait_healthy minio 60
  wait_healthy backend 180
  wait_healthy frontend 180
  smoke_test
}

cmd_down()  { log "stopping stack (keeping volumes)";   compose down; }
cmd_clean() { log "stopping stack and removing volumes"; compose down -v; }
cmd_test()  { smoke_test; }
cmd_logs()  { compose logs -f --tail=100 "${@:-}"; }

# Idempotently create a user via the public API. If the email already exists the
# register call returns 409; we swallow that and continue so the whole seed run
# is safe to invoke repeatedly.
seed_user() {
  local email=$1 password=$2 display=$3 role=${4:-learner}
  local code body
  body=$(curl -s -o /tmp/_edu_seed_body -w '%{http_code}' \
    -X POST "http://localhost:8000/api/auth/register" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$email\",\"password\":\"$password\",\"displayName\":\"$display\"}")
  code=$body
  case "$code" in
    200|201) ok "created $role '$email'" ;;
    409)     ok "$role '$email' already exists (skipped)" ;;
    *)       fail "register '$email' got HTTP $code: $(cat /tmp/_edu_seed_body 2>/dev/null)"; return 1 ;;
  esac
  if [[ "$role" == "admin" ]]; then
    compose exec -T postgres psql -U "${POSTGRES_USER:-edulingo}" -d "${POSTGRES_DB:-edulingo}" \
      -c "UPDATE users SET role='admin' WHERE email='$email';" >/dev/null
    ok "promoted '$email' to admin"
  fi
}

cmd_seed() {
  ensure_env
  set -a; source .env; set +a
  if ! curl -sf --max-time 5 http://localhost:8000/api/health >/dev/null; then
    fail "backend is not reachable at http://localhost:8000 — run '$0 up' first"
    exit 1
  fi
  log "seeding demo accounts..."
  seed_user "demo@edulingo.ai"  "password123" "Demo"  "learner"
  seed_user "admin@edulingo.ai" "admin12345"  "Admin" "admin"
  ok "seed complete"
  echo
  echo "    learner: demo@edulingo.ai / password123"
  echo "    admin:   admin@edulingo.ai / admin12345"
  echo "    login:   http://localhost:3000/login"
}

case "${1:-up}" in
  up)    cmd_up ;;
  down)  cmd_down ;;
  clean) cmd_clean ;;
  test)  cmd_test ;;
  seed)  cmd_seed ;;
  logs)  shift || true; cmd_logs "$@" ;;
  *)     fail "unknown command: $1"; echo "usage: $0 {up|down|clean|test|seed|logs}" >&2; exit 2 ;;
esac
