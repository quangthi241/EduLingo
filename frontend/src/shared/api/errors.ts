export class ApiError extends Error {
  constructor(
    public readonly title: string,
    public readonly detail: string,
    public readonly status: number,
  ) {
    super(`${title}: ${detail}`);
    this.name = "ApiError";
  }
}
