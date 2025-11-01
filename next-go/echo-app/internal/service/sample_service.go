package service

import (
	"context"
	"next-go-sample/internal/domain"
	"next-go-sample/internal/repository"
)

// SampleService provides business logic for samples
type SampleService struct {
	repo repository.SampleRepository
}

// NewSampleService creates a new sample service
func NewSampleService(repo repository.SampleRepository) *SampleService {
	return &SampleService{
		repo: repo,
	}
}

// GetAll returns all samples
func (s *SampleService) GetAll(ctx context.Context) ([]*domain.Sample, error) {
	return s.repo.FindAll(ctx)
}

// GetByID returns a sample by ID
func (s *SampleService) GetByID(ctx context.Context, id string) (*domain.Sample, error) {
	return s.repo.FindByID(ctx, id)
}

// Create creates a new sample
func (s *SampleService) Create(ctx context.Context, input *domain.CreateSampleInput) (*domain.Sample, error) {
	return s.repo.Create(ctx, input)
}

// Update updates an existing sample
func (s *SampleService) Update(ctx context.Context, id string, input *domain.UpdateSampleInput) (*domain.Sample, error) {
	return s.repo.Update(ctx, id, input)
}

// Delete deletes a sample
func (s *SampleService) Delete(ctx context.Context, id string) error {
	return s.repo.Delete(ctx, id)
}
