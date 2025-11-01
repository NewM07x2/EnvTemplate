package handler

import (
	"net/http"
	"next-go-sample/internal/domain"
	"next-go-sample/internal/service"

	"github.com/labstack/echo/v4"
)

// SampleHandler handles HTTP requests for samples
type SampleHandler struct {
	service *service.SampleService
}

// NewSampleHandler creates a new sample handler
func NewSampleHandler(service *service.SampleService) *SampleHandler {
	return &SampleHandler{
		service: service,
	}
}

// GetAll handles GET /samples
func (h *SampleHandler) GetAll(c echo.Context) error {
	samples, err := h.service.GetAll(c.Request().Context())
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, samples)
}

// GetByID handles GET /samples/:id
func (h *SampleHandler) GetByID(c echo.Context) error {
	id := c.Param("id")
	sample, err := h.service.GetByID(c.Request().Context(), id)
	if err != nil {
		return c.JSON(http.StatusNotFound, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, sample)
}

// Create handles POST /samples
func (h *SampleHandler) Create(c echo.Context) error {
	var input domain.CreateSampleInput
	if err := c.Bind(&input); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
	}

	sample, err := h.service.Create(c.Request().Context(), &input)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusCreated, sample)
}

// Update handles PUT /samples/:id
func (h *SampleHandler) Update(c echo.Context) error {
	id := c.Param("id")
	var input domain.UpdateSampleInput
	if err := c.Bind(&input); err != nil {
		return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
	}

	sample, err := h.service.Update(c.Request().Context(), id, &input)
	if err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusOK, sample)
}

// Delete handles DELETE /samples/:id
func (h *SampleHandler) Delete(c echo.Context) error {
	id := c.Param("id")
	if err := h.service.Delete(c.Request().Context(), id); err != nil {
		return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
	}
	return c.JSON(http.StatusNoContent, nil)
}
