package main

import (
	"log/slog"
	"net/http"

	"github.com/gin-gonic/gin"
)

func checkApi(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"WWII Trading Cards API Status": c.ClientIP(),
	})
}

// func getCards(c *gin.Context) {
// 	db, err := sql.Open("sqlite", "/data/trading.db")

// }

func main() {
	slog.Info("Starting WWII Trading Cards API")
	router := gin.Default()

	router.GET("/", checkApi)
	// router.GET("/cards", getCards)

	router.Run("0.0.0.0:8000")
}
