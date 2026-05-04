// ROI record returned by GET /roi
export interface ROIRecord {
    id: string
    timestamp: string
    x: number
    y: number
    width: number
    height: number
}