package repository

import (
	"context"
	"errors"
	"next-go-sample/internal/domain"
	"sync"
	"time"

	"github.com/google/uuid"
)

// InMemorySampleRepository implements SampleRepository using in-memory storage
type InMemorySampleRepository struct {
	mu      sync.RWMutex
	samples map[string]*domain.Sample
}

// NewInMemorySampleRepository creates a new in-memory sample repository
func NewInMemorySampleRepository() *InMemorySampleRepository {
	return &InMemorySampleRepository{
		samples: make(map[string]*domain.Sample),
	}
}

// FindAll returns all samples
func (r *InMemorySampleRepository) FindAll(ctx context.Context) ([]*domain.Sample, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	samples := make([]*domain.Sample, 0, len(r.samples))
	for _, sample := range r.samples {
		samples = append(samples, sample)
	}
	return samples, nil
}

// FindByID returns a sample by ID
func (r *InMemorySampleRepository) FindByID(ctx context.Context, id string) (*domain.Sample, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	sample, exists := r.samples[id]
	if !exists {
		return nil, errors.New("sample not found")
	}
	return sample, nil
}

// Create creates a new sample
func (r *InMemorySampleRepository) Create(ctx context.Context, input *domain.CreateSampleInput) (*domain.Sample, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	now := time.Now()
	sample := &domain.Sample{
		ID:        uuid.New().String(),
		Name:      input.Name,
		CreatedAt: now,
		UpdatedAt: now,
	}

	r.samples[sample.ID] = sample
	return sample, nil
}

// Update updates an existing sample
func (r *InMemorySampleRepository) Update(ctx context.Context, id string, input *domain.UpdateSampleInput) (*domain.Sample, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	sample, exists := r.samples[id]
	if !exists {
		return nil, errors.New("sample not found")
	}

	sample.Name = input.Name
	sample.UpdatedAt = time.Now()

	return sample, nil
}

// Delete deletes a sample
func (r *InMemorySampleRepository) Delete(ctx context.Context, id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.samples[id]; !exists {
		return errors.New("sample not found")
	}

	delete(r.samples, id)
	return nil
}
