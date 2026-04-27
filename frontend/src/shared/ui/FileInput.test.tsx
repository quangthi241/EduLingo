import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { FileInput } from "./FileInput";

describe("FileInput", () => {
  it("calls onFileChange with the selected file", () => {
    const onFileChange = vi.fn();
    render(
      <FileInput
        label="Audio"
        id="audio"
        accept="audio/mpeg"
        onFileChange={onFileChange}
      />,
    );
    const file = new File([new Uint8Array([1, 2])], "a.mp3", { type: "audio/mpeg" });
    fireEvent.change(screen.getByLabelText("Audio"), { target: { files: [file] } });
    expect(onFileChange).toHaveBeenCalledWith(file);
  });
});
