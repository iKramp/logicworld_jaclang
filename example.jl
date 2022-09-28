func function2() {
    var b = 20
    var a = b + 20 // 40
    return a + b // 60
}

func function() {
    var a = 30
    return 10 + a + function2() // 100
}

func main() {
    return function() + function() // 200
}