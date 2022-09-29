/// expect 100

// function test

func function() { // should return 30
    var b = 10
    var a = 20
    return a + b
}

func main() {
    var a = 20
    var b = 30 + a + function()
    return a + b
}