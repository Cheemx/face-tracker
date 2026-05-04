import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import './App.css'
import ROIHistory from './components/ROIHistory'
import VideoStream from './components/VideoStream'

const queryClient = new QueryClient()

function App() {

return (
    <QueryClientProvider client={queryClient}>
        <div className='min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white font-sans'>
            <header className="border-b border-slate-800 bg-slate-900/60 backdrop-blur-md">
                <div className="mx-auto max-w-7xl px-6 py-3 flex items-center justify-between">
                    <div>
                    <h1 className="text-sm font-semibold tracking-tight text-white">
                        Face Detection
                    </h1>
                    <p className="text-[11px] text-slate-500">
                        MediaPipe · FastAPI · Real-time WebSocket
                    </p>
                    </div>
                </div>
            </header> 

                {/* Main layout */}
            <main className="relative mx-auto max-w-7xl px-6 py-8">
                <div className="grid grid-cols-1 gap-8 lg:grid-cols-5">
                    <div className="lg:col-span-3">
                        <VideoStream />
                    </div>
                    <div className="lg:col-span-2">
                        <ROIHistory />
                    </div>
                </div>

                {/* Footer info */}
                <div className="mt-8 flex flex-wrap gap-4 text-xs text-slate-400">
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
