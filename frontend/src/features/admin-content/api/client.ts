import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import { apiFetch } from "@/shared/api/client";
import type {
  AdminListFilter,
  CreatePieceInput,
  GenerateInput,
  UpdatePieceInput,
} from "../domain/piece";
import type { Piece, PiecePage } from "@/features/library/domain/pieces";

function adminUrl(f: AdminListFilter): string {
  const p = new URLSearchParams();
  if (f.status) p.set("status", f.status);
  if (f.kind) p.set("kind", f.kind);
  if (f.cefr) p.set("cefr", f.cefr);
  if (f.topic) p.set("topic", f.topic);
  if (f.cursor) p.set("cursor", f.cursor);
  if (f.limit) p.set("limit", String(f.limit));
  const qs = p.toString();
  return qs ? `/api/admin/content?${qs}` : "/api/admin/content";
}

export function useAdminPiecesQuery(filter: AdminListFilter = {}) {
  return useQuery<PiecePage>({
    queryKey: ["admin-content", filter],
    queryFn: () => apiFetch<PiecePage>(adminUrl(filter)),
  });
}

export function useAdminPieceQuery(id: string | null) {
  return useQuery<Piece>({
    queryKey: ["admin-content", "piece", id],
    queryFn: () => apiFetch<Piece>(`/api/admin/content/${id}`),
    enabled: !!id,
  });
}

export function useCreatePieceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: CreatePieceInput) =>
      apiFetch<Piece>("/api/admin/content", {
        method: "POST",
        body: JSON.stringify(input),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}

export function useUpdatePieceMutation(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (patch: UpdatePieceInput) =>
      apiFetch<Piece>(`/api/admin/content/${id}`, {
        method: "PATCH",
        body: JSON.stringify(patch),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}

export function usePublishPieceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch<Piece>(`/api/admin/content/${id}/publish`, { method: "POST" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}

export function useArchivePieceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch<Piece>(`/api/admin/content/${id}/archive`, { method: "POST" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}

export function useDeletePieceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) =>
      apiFetch<void>(`/api/admin/content/${id}`, { method: "DELETE" }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}

export function useUploadMediaMutation(id: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const fd = new FormData();
      fd.append("file", file);
      return apiFetch<Piece>(`/api/admin/content/${id}/media`, {
        method: "POST",
        body: fd,
      });
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}

export function useGeneratePieceMutation() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (input: GenerateInput) =>
      apiFetch<Piece>("/api/admin/content/generate", {
        method: "POST",
        body: JSON.stringify({
          kind: input.kind,
          cefr: input.cefr,
          topic: input.topic,
          seedPrompt: input.seedPrompt,
        }),
      }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["admin-content"] }),
  });
}
