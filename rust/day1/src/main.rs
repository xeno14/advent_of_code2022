fn part1(input: &str) -> i32 {
    let mut tmp = 0;
    let mut ans = 0;
    for line in input.split("\n").into_iter() {
        if line.len() == 0 {
            ans = ans.max(tmp);
            tmp = 0;
        } else {
            tmp += line.parse::<i32>().unwrap();
        }
    }
    ans = ans.max(tmp);
    ans
}

fn part2(input: &str) -> i32 {
    let mut tmp = 0;
    let mut values: Vec::<i32> = Vec::new();
    for line in input.split("\n").into_iter() {
        if line.len() == 0 {
            values.push(tmp);
            tmp = 0;
        } else {
            tmp += line.parse::<i32>().unwrap();
        }
    }
    values.sort_by(|x, y| y.cmp(&x));
    values[0] + values[1] + values[2]
}

fn main() {
    assert!(part1(include_str!("../../../examples/day1.txt")) == 24000);
    println!("part1 = {}", part1(include_str!("../../../inputs/day1.txt")));
    println!("part2 = {}", part2(include_str!("../../../inputs/day1.txt")));
}