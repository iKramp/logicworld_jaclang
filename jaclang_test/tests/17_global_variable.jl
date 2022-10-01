/// expect 20

/// global variable test

var a

func function() {
    a = 20
}

func main() {
    a = 10
    function()
    return a
}
