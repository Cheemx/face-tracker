import { useROIHistory } from "../hooks/useROIHistory"
import type { ROIRecord } from "../types"

function formatTimestamp(iso: string): string {
  try {
    return new Date(iso).toLocaleTimeString(undefined, {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
    })
  } catch {
    return iso
  }
}

function ROIHistory(){
    const { data, isLoading, isError, error } = useROIHistory()

    return (
    <div className="flex flex-col gap-4 h-full">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">ROI History</h2>
        <span className="rounded-full bg-brand-500/20 border border-brand-500/30 px-2.5 py-0.5 text-xs font-medium text-brand-400">
          Last 50
        </span>
      </div>

      {/* Table container */}
      <div className="flex-1 overflow-auto rounded-xl border border-slate-700/50 bg-slate-900/60 shadow-inner">
        {isLoading && (
          <div className="flex items-center justify-center h-40 text-slate-500 text-sm">
            Loading…
          </div>
        )}

        {isError && (
          <div className="flex items-center justify-center h-40 text-red-400 text-sm">
            Error: {(error as Error).message}
          </div>
        )}

        {!isLoading && !isError && data && data.length === 0 && (
          <div className="flex items-center justify-center h-40 text-slate-600 text-sm">
            No ROI records yet. Start the webcam stream!
          </div>
        )}

        {!isLoading && !isError && data && data.length > 0 && (
          <table className="w-full text-sm">
            <thead className="sticky top-0 bg-slate-800/90 backdrop-blur-sm">
              <tr>
                {['Time', 'X', 'Y', 'Width', 'Height'].map((col) => (
                  <th
                    key={col}
                    className="px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-slate-400 border-b border-slate-700/50"
                  >
                    {col}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {data.map((record: ROIRecord) => (
                <tr
                  key={record.id}
                  className="hover:bg-slate-800/60 transition-colors duration-100 p-1 rounded-xl bg-slate-900/80"
                >
                  <td className="px-4 py-2.5 text-slate-400 font-mono text-xs">
                    {formatTimestamp(record.timestamp)}
                  </td>
                  <td className="px-4 py-2.5 text-slate-300 font-mono">{record.x}</td>
                  <td className="px-4 py-2.5 text-slate-300 font-mono">{record.y}</td>
                  <td className="px-4 py-2.5 text-slate-300 font-mono">{record.width}</td>
                  <td className="px-4 py-2.5 text-slate-300 font-mono">{record.height}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}

export default ROIHistory