/// expect 140

// more intense function test

func function1() { // should return 100
    var b = 10
    var a = 20
    var c = 20
    return a + b + c + 50
}

func function2() { // should return 90
    var b = function1() - 90
    var a = function1() + function1() - 100
    return b - a
}

func function3() { // should return 40
    var b = function2() + 20
    var a = function2() - 20
    return b - a
}

func function4() { // should return 120
    var b = function3()
    var a = 80
    return a + b
}

func test_func() {
    var a = 10
}

func main() {
    test_func()
    var a = 20
    var b = function4()
    return a + b
}