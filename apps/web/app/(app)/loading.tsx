export default function Loading() {
  return (
    <div className="flex flex-col gap-6">
      <div className="h-8 w-40 animate-pulse rounded-md bg-muted" />

      <div className="h-5 w-80 animate-pulse rounded-md bg-muted" />

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {[1, 2, 3, 4].map((item) => (
          <div
            key={item}
            className="h-24 animate-pulse rounded-xl border border-border bg-card"
          />
        ))}
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
        <div className="h-72 animate-pulse rounded-xl border border-border bg-card lg:col-span-2" />

        <div className="h-72 animate-pulse rounded-xl border border-border bg-card" />
      </div>

      <div className="h-64 animate-pulse rounded-xl border border-border bg-card" />
    </div>
  )
}