import { Suspense } from "react";

import { NewContentClient } from "./NewContentClient";

export default function Page() {
  return (
    <Suspense>
      <NewContentClient />
    </Suspense>
  );
}
