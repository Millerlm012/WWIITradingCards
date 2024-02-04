package decks

import "github.com/gin-gonic/gin"

func SetupDeckRoutes(router *gin.Engine) {
	routes := router.Group("/decks")
	{
		routes.GET("/", GetAllDecks)
	}
}
