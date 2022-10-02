/// expect 55

/// while fibonacci test

func main() {
    var a = 0
    var b = 1

    var i = 0
    while i < 10 {
        var c = a + b
        a = b
        b = c
        i = i + 1
    }
    return a
}