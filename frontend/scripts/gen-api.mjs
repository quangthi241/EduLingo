import { execSync } from "node:child_process";

execSync("curl -fsS http://localhost:8000/api/openapi.json -o openapi.json", {
  stdio: "inherit",
});
execSync(
  "pnpm dlx openapi-typescript openapi.json -o src/shared/api/generated/schema.ts",
  { stdio: "inherit" },
);
