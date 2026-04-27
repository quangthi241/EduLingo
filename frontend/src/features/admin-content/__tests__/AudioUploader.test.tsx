import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";

import { AudioUploader } from "../ui/AudioUploader";

describe("AudioUploader", () => {
  it("rejects non-audio mime types", async () => {
    const onUpload = vi.fn();
    render(<AudioUploader onUpload={onUpload} />);
    const input = screen.getByLabelText(/audio file/i);
    const file = new File([new Uint8Array([1])], "x.txt", { type: "text/plain" });
    fireEvent.change(input, { target: { files: [file] } });
    expect(await screen.findByRole("alert")).toHaveTextContent(/audio/i);
    expect(onUpload).not.toHaveBeenCalled();
  });

  it("calls onUpload with valid audio", () => {
    const onUpload = vi.fn();
    render(<AudioUploader onUpload={onUpload} />);
    const input = screen.getByLabelText(/audio file/i);
    const file = new File([new Uint8Array([1])], "x.mp3", { type: "audio/mpeg" });
    fireEvent.change(input, { target: { files: [file] } });
    expect(onUpload).toHaveBeenCalledWith(file);
  });
});
