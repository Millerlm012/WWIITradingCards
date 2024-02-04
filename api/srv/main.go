package main

import (
	"log/slog"
	"net/http"
	"wwii_cards/api/cards"
	"wwii_cards/api/decks"
	"wwii_cards/api/images"
	"wwii_cards/api/utils"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	_ "github.com/glebarez/go-sqlite"
)

func checkApi(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"WWII Trading Cards API Status": c.ClientIP(),
	})
}

func main() {
	slog.Info("Connecting to database.")
	utils.ConnectDatabase()
	slog.Info(`Connected sucessfully!`)

	slog.Info("Starting WWII Trading Cards API")
	router := gin.Default()
	wwiiCors := utils.GetCors()
	router.Use(cors.New(wwiiCors))

	router.GET("/", checkApi)
	images.SetupImageRoutes(router)
	cards.SetupCardRoutes(router)
	decks.SetupDeckRoutes(router)

	router.Run("0.0.0.0:8000")
}
