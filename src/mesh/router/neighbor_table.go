package router

import "sync"

type Neighbor struct {
	NodeID string
	EID    string
	LQI    float64
}

type NeighborTable struct {
	mu        sync.RWMutex
	neighbors map[string]Neighbor
}

func NewNeighborTable() *NeighborTable {
	return &NeighborTable{neighbors: map[string]Neighbor{}}
}

func (t *NeighborTable) Upsert(n Neighbor) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.neighbors[n.NodeID] = n
}

func (t *NeighborTable) Snapshot() []Neighbor {
	t.mu.RLock()
	defer t.mu.RUnlock()
	out := make([]Neighbor, 0, len(t.neighbors))
	for _, n := range t.neighbors {
		out = append(out, n)
	}
	return out
}
