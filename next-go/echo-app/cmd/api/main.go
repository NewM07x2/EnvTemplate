package main

import (
	"log"
	"next-go-sample/internal/config"
	"next-go-sample/internal/handler"
	"next-go-sample/internal/repository"
	"next-go-sample/internal/router"
	"next-go-sample/internal/service"

	"github.com/labstack/echo/v4"
)

func main() {
	// Load configuration
	cfg := config.Load()

	// Initialize Echo
	e := echo.New()

	// Initialize repositories
	sampleRepo := repository.NewInMemorySampleRepository()

	// Initialize services
	sampleService := service.NewSampleService(sampleRepo)

	// Initialize handlers
	healthHandler := handler.NewHealthHandler()
	sampleHandler := handler.NewSampleHandler(sampleService)

	// Setup routes
	router.SetupRoutes(e, healthHandler, sampleHandler)

	// Start server
	log.Printf("Starting server on port %s", cfg.Port)
	if err := e.Start(":" + cfg.Port); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
