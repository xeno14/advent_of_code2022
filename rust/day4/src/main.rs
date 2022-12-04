#[derive(Debug, PartialEq)]
struct Range(i32, i32);

impl Range {
    fn from_str(s: &str) -> Range {
        let pieces: Vec<&str> = s.split('-').collect();
        Range(
            pieces[0].parse::<i32>().unwrap(),
            pieces[1].parse::<i32>().unwrap(),
        )
    }

    fn contains_range(&self, other: &Range) -> bool {
        self.0 <= other.0 && other.1 <= self.1
    }

    fn contains(&self, x: i32) -> bool {
        self.0 <= x && x <= self.1
    }

    fn overwraps(&self, other: &Range) -> bool {
        self.contains(other.0)
            || self.contains(other.1)
            || other.contains(self.0)
            || other.contains(self.1)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_from_str() {
        assert_eq!(Range(12, 345), Range::from_str("12-345"))
    }

    #[test]
    fn test_contains_range() {
        assert!(Range(2, 8).contains_range(&Range(3, 7)));
        assert!(Range(4, 6).contains_range(&Range(6, 6)));
        assert!(!Range(2, 4).contains_range(&Range(5, 6)));
    }

    #[test]
    fn test_overwraps() {
        assert!(Range(5, 7).overwraps(&Range(7, 9)));
        assert!(!Range(2, 3).overwraps(&Range(4, 6)));
    }
}

fn parse(input: &str) -> Vec<(Range, Range)> {
    input
        .split('\n')
        .map(|line| {
            let pieces: Vec<&str> = line.split(',').collect();
            (Range::from_str(pieces[0]), Range::from_str(pieces[1]))
        })
        .collect()
}

fn part1(input: &str) -> usize {
    parse(input)
        .iter()
        .filter(|(x, y)| x.contains_range(y) || y.contains_range(x))
        .count()
}

fn part2(input: &str) -> usize {
    parse(input).iter().filter(|(x, y)| x.overwraps(y)).count()
}

fn main() {
    assert!(part1(include_str!("../../../examples/day4.txt")) == 2);
    println!(
        "part1 = {}",
        part1(include_str!("../../../inputs/day4.txt"))
    );
    println!(
        "part2 = {}",
        part2(include_str!("../../../inputs/day4.txt"))
    );
}
