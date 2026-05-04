// ROI record returned by GET /roi
export interface ROIRecord {
    id: string
    timestamp: string
    x: number
    y: number
    width: number
    height: number
}

// Region of Interest.
export interface ROI {
    x: number
    y: number
    width: number
    height: number
}

// WebSocket response message from the ws connection
export interface WSMessage {
    frame: string   // base64-encoded annotated JPEG
    roi: ROI | null // null when no face detected
    error?: string
}