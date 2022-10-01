/// expect 55

/// fibonacci with ugly global variable workaround

var param

func fib() {
    if param < 2
        return param
    var par = param
    param = par - 1
    var a = fib()
    param = par - 2
    var b = fib()
    return a + b
}

func main() {
    param = 10
    return fib()
}