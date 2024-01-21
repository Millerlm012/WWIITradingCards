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

func main() {
	slog.Info("Starting WWII Trading Cards API")
	router := gin.Default()

	router.GET("/", checkApi)

	router.Run("0.0.0.0:8000")
}
