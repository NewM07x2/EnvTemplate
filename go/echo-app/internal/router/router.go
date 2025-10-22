package router

import (
	"next-go-sample/internal/handler"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

// SetupRoutes configures all application routes
func SetupRoutes(e *echo.Echo, healthHandler *handler.HealthHandler, sampleHandler *handler.SampleHandler) {
	// Middleware
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())
	e.Use(middleware.CORS())

	// Health check
	e.GET("/health", healthHandler.Check)

	// API v1 routes
	v1 := e.Group("/api/v1")
	{
		// Sample routes
		samples := v1.Group("/samples")
		samples.GET("", sampleHandler.GetAll)
		samples.GET("/:id", sampleHandler.GetByID)
		samples.POST("", sampleHandler.Create)
		samples.PUT("/:id", sampleHandler.Update)
		samples.DELETE("/:id", sampleHandler.Delete)
	}
}
