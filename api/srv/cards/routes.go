package cards

import "github.com/gin-gonic/gin"

func SetupCardRoutes(router *gin.Engine) {
	routes := router.Group("/cards")
	{
		routes.GET("/:deckId", GetCards)
	}
}
