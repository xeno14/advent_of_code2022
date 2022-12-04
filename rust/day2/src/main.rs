enum MyHand {
    X,
    Y,
    Z,
}
enum TheirHand {
    A,
    B,
    C,
}

fn parse(input: &str) -> Vec<(TheirHand, MyHand)> {
    input
        .lines()
        .map(|line| {
            let their_hand: TheirHand = match line.chars().nth(0).unwrap() {
                'A' => TheirHand::A,
                'B' => TheirHand::B,
                'C' => TheirHand::C,
                _ => panic!("unreachable"),
            };
            let my_hand: MyHand = match line.chars().nth(2).unwrap() {
                'X' => MyHand::X,
                'Y' => MyHand::Y,
                'Z' => MyHand::Z,
                _ => panic!("unreachable"),
            };
            (their_hand, my_hand)
        })
        .collect()
}

fn part1(input: &str) -> i32 {
    let hands = parse(input);

    hands
        .iter()
        .map(|(theirs, mine)| {
            let outcome_point = match (theirs, mine) {
                // Opponent: Rock
                (TheirHand::A, MyHand::X) => 3,
                (TheirHand::A, MyHand::Y) => 6,
                (TheirHand::A, MyHand::Z) => 0,
                // Opponent: Paper
                (TheirHand::B, MyHand::X) => 0,
                (TheirHand::B, MyHand::Y) => 3,
                (TheirHand::B, MyHand::Z) => 6,
                // Opponent: Scisors
                (TheirHand::C, MyHand::X) => 6,
                (TheirHand::C, MyHand::Y) => 0,
                (TheirHand::C, MyHand::Z) => 3,
            };
            let my_hand_point = match mine {
                MyHand::X => 1,
                MyHand::Y => 2,
                MyHand::Z => 3,
            };
            outcome_point + my_hand_point
        })
        .sum()
}

fn do_part2_round(theirs: &TheirHand, mine: &MyHand) -> i32 {
    // My hand represents outcome.
    let outcome_point = match mine {
        MyHand::X => 0,
        MyHand::Y => 3,
        MyHand::Z => 6,
    };
    // Convert my hand accordingly.
    let my_hand_point: i32 = match (theirs, mine) {
        // Opponent: Rock
        (TheirHand::A, MyHand::X) => 3, // Scisors
        (TheirHand::A, MyHand::Y) => 1, // Rock
        (TheirHand::A, MyHand::Z) => 2, // Paper
        // Opponent: Paper
        (TheirHand::B, MyHand::X) => 1, // Rock
        (TheirHand::B, MyHand::Y) => 2, // Paper
        (TheirHand::B, MyHand::Z) => 3, // Scisors
        // Opponent: Scisors
        (TheirHand::C, MyHand::X) => 2, // Paper
        (TheirHand::C, MyHand::Y) => 3, // Scisors
        (TheirHand::C, MyHand::Z) => 1, // Rock
    };
    outcome_point + my_hand_point
}

fn part2(input: &str) -> i32 {
    let hands = parse(input);

    hands.iter().map(|(x, y)| do_part2_round(x, y)).sum()
}

fn main() {
    assert!(part1(include_str!("../../../examples/day2.txt")) == 15);
    println!(
        "part1 = {}",
        part1(include_str!("../../../inputs/day2.txt"))
    );
    assert!(part2(include_str!("../../../examples/day2.txt")) == 12);
    println!("part2 = {}", part2(include_str!("../../../inputs/day2.txt")));
}
