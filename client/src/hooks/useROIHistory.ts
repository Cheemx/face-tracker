import { useQuery } from "@tanstack/react-query";
import type { ROIRecord } from "../types";
import { fetchROIHistory } from "../api/api";

export function useROIHistory() {
    return useQuery<ROIRecord[], Error>({
        queryKey: ['roi-history'],
        queryFn: fetchROIHistory,
        refetchInterval: 2000,
        staleTime: 1000
    })
}