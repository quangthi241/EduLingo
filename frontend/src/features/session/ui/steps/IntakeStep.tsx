export function IntakeStep() {
  return (
    <div className="flex flex-col gap-6">
      <p className="caption">
        Read at your own pace. You can click any word for a gloss.
      </p>
      <article className="prose-editorial">
        <p>
          The shoreline looks firm from a distance, but it is in constant
          negotiation with the sea. Every wave carries off a little of
          what was here: grains of sand, the crumble of a dune,
          occasionally an entire house set too close to the edge.
        </p>
        <p>
          <em>By the time</em> the municipal maps had caught up with the
          erosion at Sable Point, the coastline had already moved eleven
          metres inland &mdash; a decade of change condensed into a
          single resurvey. What had once been the end of a road was now
          ten metres out at sea.
        </p>
        <p>
          Coastal engineers are beginning to accept that no seawall is a
          permanent answer. Soft mitigation &mdash; restored dunes,
          planted grasses, sediment replenished each spring &mdash;
          turns out to outperform concrete over the long run.
        </p>
      </article>
      <aside className="surface-sunken flex flex-col gap-2 p-4">
        <p className="eyebrow">Words to watch for</p>
        <p className="font-display text-lg italic text-[color:var(--color-ink)]">
          erode &middot; sediment &middot; mitigation
        </p>
      </aside>
    </div>
  );
}
