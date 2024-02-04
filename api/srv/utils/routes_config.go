package utils

import (
	"os"

	"github.com/gin-contrib/cors"
)

func GetCors() cors.Config {
	env := os.Getenv("ENV")

	wwiiCors := cors.DefaultConfig()
	if env == "dev" {
		wwiiCors = cors.Config{
			AllowOrigins:     []string{"*"},
			AllowMethods:     []string{"*"},
			AllowHeaders:     []string{"*"},
			ExposeHeaders:    []string{"Content-Length"},
			AllowCredentials: true,
		}
	} else if env == "prod" {
		// TODO: verify that the following CORS are secure and work in production
		wwiiCors = cors.Config{
			AllowOrigins:     []string{"https://wwii-trading-cards.com/"},
			AllowMethods:     []string{"GET"},
			AllowHeaders:     []string{"Origin"},
			AllowCredentials: true,
		}
	} else {
		panic("Not a valid env!")
	}

	return wwiiCors
}
