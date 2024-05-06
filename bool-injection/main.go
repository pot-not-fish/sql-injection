package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
)

type User struct {
	Username string
	Password string
}

type Student struct {
	Name string
	Age  int
}

var db *gorm.DB

// 连接数据库
func Init() {
	var err error

	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags),
		logger.Config{
			SlowThreshold: time.Microsecond,
			LogLevel:      logger.Info,
		},
	)

	username := "root" // 使用者名字 如root
	password := "123456"
	host := "127.0.0.1"
	port := 3306
	dbname := "test" // 数据库名字
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8&parseTime=True&loc=Local", username, password, host, port, dbname)

	db, err = gorm.Open(mysql.Open(dsn), &gorm.Config{
		Logger: newLogger, // 将SQL信息打印到终端
		DryRun: false,
	})
	if err != nil {
		panic(err)
	}
	db.AutoMigrate(&User{}, &Student{})
}

type UserReq struct {
	Username string `form:"username" json:"username" xml:"username"`
	Password string `form:"password" json:"password" xml:"password"`
}

// search业务逻辑处理
func Search(c *gin.Context) {
	var (
		err     error
		userReq UserReq
	)
	if err := c.ShouldBind(&userReq); err != nil {
		c.JSON(http.StatusOK, gin.H{"code": 1, "msg": "invalid paramenter"})
		return
	}

	// 查询用户名是否正确
	var user User
	stmt := db.Where(fmt.Sprintf("username = '%v' AND password = '%v'", userReq.Username, userReq.Password)).First(&user).Statement
	fmt.Println(db.Dialector.Explain(stmt.SQL.String(), stmt.Vars...))
	if err = db.Where(fmt.Sprintf("username = '%v' AND password = '%v'", userReq.Username, userReq.Password)).First(&user).Error; err != nil {
		c.JSON(http.StatusOK, gin.H{"code": 1, "msg": "invalid parameters"})
		return
	}

	// 查询用户名信息
	var student Student
	stmt = db.Where(fmt.Sprintf("name = '%v'", user.Username)).First(&Student{}).Statement
	fmt.Println(db.Dialector.Explain(stmt.SQL.String(), stmt.Vars...))
	if err = db.Where(fmt.Sprintf("name = '%v'", user.Username)).First(&student).Error; err != nil {
		c.JSON(http.StatusOK, gin.H{"code": 1, "msg": "invalid username or password"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"code": 0, "msg": "ok", "name": student.Name, "age": student.Age})
}

func main() {
	Init()

	// 开启网络服务
	r := gin.Default()
	r.POST("/search", Search) // 访问127.0.0.1/search
	r.Run("127.0.0.1:8080")
}
