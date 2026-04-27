"use client";

import { useState } from "react";

import { FileInput } from "@shared/ui/FileInput";

type Props = {
  onUpload: (file: File) => void;
  uploading?: boolean;
};

const ALLOWED = ["audio/mpeg", "audio/mp4", "audio/wav", "audio/ogg"];

export function AudioUploader({ onUpload, uploading }: Props) {
  const [error, setError] = useState<string | null>(null);

  function handle(file: File | null) {
    setError(null);
    if (!file) return;
    if (!ALLOWED.includes(file.type)) {
      setError("File must be an audio file (mp3, m4a, wav, ogg).");
      return;
    }
    if (file.size > 50 * 1024 * 1024) {
      setError("File must be 50 MB or smaller.");
      return;
    }
    onUpload(file);
  }

  return (
    <div className="flex flex-col gap-2">
      <FileInput
        id="audio-upload"
        label="Audio file"
        accept="audio/*"
        onFileChange={handle}
        disabled={uploading}
      />
      {uploading && (
        <p role="status" aria-live="polite" className="text-xs text-ink-muted">
          Uploading …
        </p>
      )}
      {error && (
        <p role="alert" className="text-xs text-danger">
          {error}
        </p>
      )}
    </div>
  );
}
