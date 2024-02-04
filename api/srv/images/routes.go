package images

import "github.com/gin-gonic/gin"

func SetupImageRoutes(router *gin.Engine) {
	routes := router.Group("/images")
	{
		routes.GET("/image", GetImage)
	}
}
