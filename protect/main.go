package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
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

func (u *UserReq) Filter() {
	u.Username = strings.Replace(u.Username, "/**/", "", -1)
	u.Username = strings.Replace(u.Username, "select", "", -1)
	u.Username = strings.Replace(u.Username, "union", "", -1)
	u.Username = strings.Replace(u.Username, "length", "", -1)
	u.Username = strings.Replace(u.Username, "information_schema", "", -1)

	u.Password = strings.Replace(u.Password, "/**/", "", -1)
	u.Password = strings.Replace(u.Password, "select", "", -1)
	u.Password = strings.Replace(u.Password, "union", "", -1)
	u.Password = strings.Replace(u.Password, "length", "", -1)
	u.Password = strings.Replace(u.Password, "information_schema", "", -1)

	fmt.Printf("过滤后的username %v\n", u.Username)
	fmt.Printf("过滤后的password %v\n", u.Password)
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

	// 过滤可能存在的SQL注入语句
	userReq.Filter()

	// 查询用户名是否正确
	var user User
	// Where(fmt.Sprintf("username = '%v' AND password = '%v'", userReq.Username, userReq.Password)) 直接使用格式化字符串会有字符转义注入的风险
	stmt := db.Where("username = ? and password = ?", userReq.Username, userReq.Password).First(&user).Statement
	fmt.Println(db.Dialector.Explain(stmt.SQL.String(), stmt.Vars...))
	if err = db.Where("username = ? and password = ?", userReq.Username, userReq.Password).First(&user).Error; err != nil {
		c.JSON(http.StatusOK, gin.H{"code": 1, "msg": "username or password is wrong"}) // 数据库的错误信息不能直接返回给用户
		return
	}

	// 查询用户名信息
	var student Student
	// Where(fmt.Sprintf("name = '%v'", user.Username)) 直接使用格式化字符串会有字符转义注入的风险
	stmt = db.Where("name = ?", user.Username).First(&Student{}).Statement
	fmt.Println(db.Dialector.Explain(stmt.SQL.String(), stmt.Vars...))
	if err = db.Where("name = ?", user.Username).First(&student).Error; err != nil {
		c.JSON(http.StatusOK, gin.H{"code": 1, "msg": "can not found user"}) // 数据库的错误信息不能直接返回给用户
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
