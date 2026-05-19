package router

import "sync"

type Bundle struct {
	ID      string
	Payload []byte
	Encrypted bool
}

type Forwarder struct {
	in    chan Bundle
	out   chan Bundle
	wg    sync.WaitGroup
	close chan struct{}
}

func NewForwarder(buffer int) *Forwarder {
	f := &Forwarder{in: make(chan Bundle, buffer), out: make(chan Bundle, buffer), close: make(chan struct{})}
	f.wg.Add(1)
	go func() {
		defer f.wg.Done()
		for {
			select {
			case b := <-f.in:
				f.out <- b
			case <-f.close:
				return
			}
		}
	}()
	return f
}

func (f *Forwarder) Submit(bundle Bundle) { f.in <- bundle }
func (f *Forwarder) Output() <-chan Bundle { return f.out }
func (f *Forwarder) Stop() {
	close(f.close)
	f.wg.Wait()
}
