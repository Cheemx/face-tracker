import axios from "axios";
import type { ROIRecord } from "../types";

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function fetchROIHistory(): Promise<ROIRecord[]> {
    const response = await axios.get(`${API_BASE}/roi`)
    if (response.status != 200) {
        throw new Error(`Failed to fetch ROI history: ${response.statusText}`)
    }
    return response.data
}