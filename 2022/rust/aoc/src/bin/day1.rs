const INPUTS: [&str; 2] = ["./inputs/1.test", "./inputs/1.input"];

fn part2(input: &String) -> i64 {
    let sums = input
        .split("\n\n")
        .map(|e| e.lines().map(|n| n.parse::<i64>().unwrap()).sum::<i64>());
    let mut max1 = 0;
    let mut max2 = 0;
    let mut max3 = 0;
    for sum in sums {
        if sum > max1 {
            max3 = max2;
            max2 = max1;
            max1 = sum;
        } else if sum > max2 {
            max3 = max2;
            max2 = sum;
        } else if sum > max3 {
            max3 = sum;
        }
    }

    max1 + max2 + max3
}

fn part1(input: &String) -> i64 {
    input.split("\n\n").fold(0, |acc, e| {
        std::cmp::max(
            e.lines().map(|n| n.parse::<i64>().unwrap()).sum::<i64>(),
            acc,
        )
    })
}

fn solution_helper(input_file: &'static str) -> (i64, i64) {
    let input = std::fs::read_to_string(input_file).expect("Unable to open file!");

    (part1(&input), part2(&input))
}

fn main() {
    for input in INPUTS {
        println!("{:?}", solution_helper(input));
    }
}
