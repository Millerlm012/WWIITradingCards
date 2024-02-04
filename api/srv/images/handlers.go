package images

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func GetImage(c *gin.Context) {
	imageUrl := c.Query("imageUrl")

	if imageUrl == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Need to specify image url as a query param"})
		return
	}

	c.File(imageUrl)
}
