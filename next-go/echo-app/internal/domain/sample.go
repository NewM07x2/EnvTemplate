package domain

import "time"

// Sample represents a sample entity
type Sample struct {
	ID        string    `json:"id"`
	Name      string    `json:"name"`
	CreatedAt time.Time `json:"createdAt"`
	UpdatedAt time.Time `json:"updatedAt"`
}

// CreateSampleInput represents input for creating a sample
type CreateSampleInput struct {
	Name string `json:"name" validate:"required"`
}

// UpdateSampleInput represents input for updating a sample
type UpdateSampleInput struct {
	Name string `json:"name" validate:"required"`
}
