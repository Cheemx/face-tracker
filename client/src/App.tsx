import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './App.css'
import ROIHistory from './components/ROIHistory'

const queryClient = new QueryClient()

function App() {

return (
    <QueryClientProvider client={queryClient}>
        <div className='min-h-screen bg-gradient-to-br text-white font-sans'>
            <header className="relative border-b backdrop-blur-md">
                <div className="mx-auto max-w-7xl px-6 py-4 flex items-center gap-4">
                    {/* Logo mark */}
                    <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-brand-500 to-brand-600 shadow-lg shadow-brand-500/20">
                        <svg className="h-5 w-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                        />
                        </svg>
                    </div>
                    <div>
                        <h1 className="text-base font-bold tracking-tight text-white">
                            Face Detection
                        </h1>
                        <p className="text-xs text-slate-500">MediaPipe · FastAPI · Real-time WebSocket</p>
                    </div>
                </div>
            </header>  

                {/* Main layout */}
            <main className="relative mx-auto max-w-7xl px-6 py-8">
                <div className="grid grid-cols-1 gap-8 lg:grid-cols-5">
                    <div className="lg:col-span-2">
                        <ROIHistory />
                    </div>
                </div>

                {/* Footer info */}
                <div className="mt-8 flex flex-wrap gap-4 text-xs text-slate-600">
                    <span>Backend: <span className="text-slate-500 font-mono">localhost:8000</span></span>
                    <span>WebSocket: <span className="text-slate-500 font-mono">ws://localhost:8000/ws/video</span></span>
                    <span>DB: <span className="text-slate-500 font-mono">PostgreSQL · rois table</span></span>
                </div>
            </main>    
        </div>
    </QueryClientProvider>
)
}

export default App
