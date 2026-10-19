/**
 * Constants, formatters, and metadata mappings for PyPulse Daily
 */

const TOPIC_METADATA = {
  "Variables & Math": {
    icon: "fa-calculator",
    color: "from-blue-500 to-indigo-600",
    badge: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    description: "Numbers, expressions, type casting, arithmetic precedence"
  },
  "Strings": {
    icon: "fa-font",
    color: "from-teal-500 to-emerald-600",
    badge: "bg-teal-500/10 text-teal-400 border-teal-500/20",
    description: "Slicing, formatting, immutability, string methods"
  },
  "Conditionals": {
    icon: "fa-code-branch",
    color: "from-amber-500 to-orange-600",
    badge: "bg-amber-500/10 text-amber-400 border-amber-500/20",
    description: "Boolean logic, if/elif/else, comparisons, truthiness"
  },
  "Loops & Iterations": {
    icon: "fa-rotate",
    color: "from-purple-500 to-pink-600",
    badge: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    description: "for/while loops, range, enumerate, break/continue"
  },
  "Lists & Tuples": {
    icon: "fa-list-ol",
    color: "from-cyan-500 to-blue-600",
    badge: "bg-cyan-500/10 text-cyan-400 border-cyan-500/20",
    description: "Sequence methods, sorting, slicing, comprehensions"
  },
  "Dictionaries & Sets": {
    icon: "fa-book-bookmark",
    color: "from-emerald-500 to-teal-600",
    badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    description: "Key-value mapping, set uniqueness, hash lookups"
  },
  "Functions & Logic": {
    icon: "fa-gears",
    color: "from-violet-500 to-indigo-600",
    badge: "bg-violet-500/10 text-violet-400 border-violet-500/20",
    description: "Parameters, return statements, scope, recursion"
  },
  "Basic Algorithms": {
    icon: "fa-brain",
    color: "from-rose-500 to-red-600",
    badge: "bg-rose-500/10 text-rose-400 border-rose-500/20",
    description: "Two pointers, accumulators, stacks, complexity"
  }
};

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

function formatDuration(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  if (m === 0) return `${s}s`;
  return `${m}m ${s}s`;
}

function getSkillLevel(scoreSum, testsCompleted) {
  if (testsCompleted === 0) return "Novice";
  const avg = scoreSum / testsCompleted;
  if (avg >= 4.5) return "Pythonista";
  if (avg >= 3.5) return "Practitioner";
  if (avg >= 2.5) return "Apprentice";
  return "Novice";
}
