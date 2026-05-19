package router

import "sync/atomic"

type Metrics struct {
	BundlesForwarded uint64
	BundlesDropped   uint64
}

func (m *Metrics) IncForwarded() { atomic.AddUint64(&m.BundlesForwarded, 1) }
func (m *Metrics) IncDropped()   { atomic.AddUint64(&m.BundlesDropped, 1) }
