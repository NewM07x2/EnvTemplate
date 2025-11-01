package repository

import (
	"context"
	"next-go-sample/internal/domain"
)

// SampleRepository defines the interface for sample data access
type SampleRepository interface {
	FindAll(ctx context.Context) ([]*domain.Sample, error)
	FindByID(ctx context.Context, id string) (*domain.Sample, error)
	Create(ctx context.Context, input *domain.CreateSampleInput) (*domain.Sample, error)
	Update(ctx context.Context, id string, input *domain.UpdateSampleInput) (*domain.Sample, error)
	Delete(ctx context.Context, id string) error
}
