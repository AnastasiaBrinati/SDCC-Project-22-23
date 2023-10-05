package main

import (
	_ "frontend/routers"
	"github.com/astaxie/beego"
	"github.com/astaxie/beego/session"
)

func main() {
	sessionconf := &session.ManagerConfig{
		CookieName:     "beegosessionID",
		Gclifetime:     3600,
		ProviderConfig: "./tmp",
	}
	beego.GlobalSessions, _ = session.NewManager("file", sessionconf)
	go beego.GlobalSessions.GC()

	beego.Run()

}