import { useCallback, useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import type { WSMessage, ROI } from "../types";

const WS_URL = import.meta.env.VITE_WS_URL ?? 'ws://localhost:8000/ws/video'
const FRAME_INTERVAL_MS = 200

type ConnectionStatus = 'connecting' | 'connected' | 'disconnected' | 'error'

export default function VideoStream() {
    const webCamRef = useRef<Webcam>(null)
    const wsRef = useRef<WebSocket | null>(null)
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

    const [processedFrame, setProcessedFrame] = useState<string | null>(null)
    const [currentROI, setCurrentROI] = useState<ROI | null>(null)
    const [status, setStatus] = useState<ConnectionStatus>('connecting')
    const [frameCount, setFrameCount] = useState(0)
    
    const connect = useCallback(() => {
        setStatus('connecting')
        const ws = new WebSocket(WS_URL)
        wsRef.current = ws

        ws.onopen = () => {
            setStatus('connected')
        }

        ws.onmessage = (event: MessageEvent) => {
            try {
                const msg: WSMessage = JSON.parse(event.data as string)
                if (msg.error) return
                setProcessedFrame(msg.frame)
                setCurrentROI(msg.roi)
                setFrameCount((c) => c+1)
            } catch {
                // Ignore malformed messages
            }
        }

        ws.onerror = () => setStatus('error')

        ws.onclose = () => {
            setStatus('disconnected')
            setTimeout(connect, 3000)
        }
    }, [])

    useEffect(() => {
        connect()
        return () => {
            wsRef.current?.close()
            if (intervalRef.current) clearInterval(intervalRef.current)
        }
    }, [connect])

    useEffect(() => {
        if (status !== 'connected') {
            if (intervalRef.current) clearInterval(intervalRef.current)
            return
        }

        intervalRef.current = setInterval(() => {
            const ws = wsRef.current
            if (!ws || ws.readyState !== WebSocket.OPEN) return

            const screenshot = webCamRef.current?.getScreenshot()
            if (!screenshot) return

            ws.send(JSON.stringify({ frame: screenshot }))
        }, FRAME_INTERVAL_MS)

        return () => {
            if (intervalRef.current) clearInterval(intervalRef.current)
        }
    }, [status])

    const statusConfig: Record<ConnectionStatus, { label: string; classes: string }> = {
        connecting: { label: 'Connecting…', classes: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30' },
        connected: { label: 'Live', classes: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' },
        disconnected: { label: 'Reconnecting…', classes: 'bg-slate-500/20 text-slate-400 border-slate-500/30' },
        error: { label: 'Error', classes: 'bg-red-500/20 text-red-400 border-red-500/30' },
    }

    const badge = statusConfig[status]

    return (
        <div className="flex flex-col gap-4">
      {/* Header row */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-white">Live Feed</h2>
        <div className="flex items-center gap-3">
          <span className="text-xs text-slate-500">Frames: {frameCount}</span>
          <span
            className={`flex items-center gap-1.5 rounded-full border px-3 py-1 text-xs font-medium ${badge.classes}`}
          >
            {status === 'connected' && (
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
            )}
            {badge.label}
          </span>
        </div>
      </div>

      {/* Video display area */}
      <div className="relative rounded-xl overflow-hidden border border-slate-700/50 bg-slate-900 shadow-2xl aspect-video">
        {/* Hidden webcam — used only for frame capture */}
        <Webcam
          ref={webCamRef}
          audio={false}
          screenshotFormat="image/jpeg"
          screenshotQuality={0.85}
          className="absolute inset-0 w-full h-full object-cover opacity-0 pointer-events-none"
          videoConstraints={{ facingMode: 'user', width: 640, height: 480 }}
        />

        {/* Processed annotated frame from backend */}
        {processedFrame ? (
          <img
            src={processedFrame}
            alt="Processed frame with face detection bounding box"
            className="w-full h-full object-cover transition-opacity duration-200"
            style={{ opacity: processedFrame ? 1 : 0 }}
          />
        ) : (
          <div className="flex items-center justify-center w-full h-full text-slate-600">
            <div className="text-center">
              <svg className="mx-auto mb-3 h-12 w-12 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5}
                  d="M15 10l4.553-2.069A1 1 0 0121 8.82v6.36a1 1 0 01-1.447.894L15 14M3 8a2 2 0 012-2h10a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V8z"
                />
              </svg>
              <p className="text-sm">Waiting for video stream…</p>
            </div>
          </div>
        )}

        {/* ROI badge overlay (informational) */}
        {currentROI && (
          <div className="absolute bottom-3 left-3 rounded-lg bg-black/60 backdrop-blur-sm border border-emerald-500/30 px-3 py-1.5 text-xs text-emerald-400 font-mono">
            Face @ ({currentROI.x}, {currentROI.y}) &nbsp;|&nbsp; {currentROI.width}×{currentROI.height}px
          </div>
        )}

        {/* No-face indicator */}
        {processedFrame && !currentROI && (
          <div className="absolute bottom-3 left-3 rounded-lg bg-black/60 backdrop-blur-sm border border-slate-600/30 px-3 py-1.5 text-xs text-slate-500">
            No face detected
          </div>
        )}
      </div>
    </div>
    )
}
