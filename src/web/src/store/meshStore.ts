import { create } from "zustand";

export type MeshMessage = { id: string; to: string; text: string; status: string; encrypted?: boolean };
export type Neighbor = { node_id: string; eid: string; lqi: number };

interface MeshState {
  neighbors: Neighbor[];
  messages: MeshMessage[];
  nodeStatus: { routing_strategy: string; store_depth: number; battery: string };
  setNeighbors: (neighbors: Neighbor[]) => void;
  addMessage: (m: MeshMessage) => void;
  setNodeStatus: (status: MeshState["nodeStatus"]) => void;
}

export const useMeshStore = create<MeshState>((set) => ({
  neighbors: [],
  messages: [],
  nodeStatus: { routing_strategy: "epidemic", store_depth: 0, battery: "unknown" },
  setNeighbors: (neighbors) => set({ neighbors }),
  addMessage: (m) => set((s) => ({ messages: [m, ...s.messages] })),
  setNodeStatus: (nodeStatus) => set({ nodeStatus })
}));
