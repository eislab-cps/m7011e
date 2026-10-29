# Grade 5: Scientific Experiments and an Advanced Test Harness

Grade 5 builds on **all Grade 4 requirements**. It requires rigorous quantitative evaluation of your application: a question, a controlled experiment, reproducible evidence and a conclusion supported by the results. An advanced feature, a coverage percentage or a screenshot of one load test is not sufficient on its own.

The core assignment already requires a load-generation tool and performance analysis under REQ17–REQ18. For Grade 5, turn that work into a scientific study. Use an advanced test harness to make it repeatable. Choose a coherent evaluation of scalability, resilience/high availability, an advanced feature, or an advanced testing strategy. You do not need to study every area.

## What Does Scientific Rigor Mean?

Scientific rigor means making a claim that can be challenged, using a method another team can inspect and repeat. It does not mean producing a positive result at any cost.

| Element | What to write down | Booking-system example |
| --- | --- | --- |
| Question | A specific uncertainty about the application. | Does a second API replica improve latency under a given load? |
| Hypothesis | A measurable prediction that results could contradict. | Two replicas reduce p95 latency without increasing errors beyond our stated bound. |
| Baseline | The comparison configuration. | One replica, with the same image, database and dataset. |
| Independent variable | What you deliberately change. | API replica count. |
| Outcomes | Measurements, including correctness. | Latency, completed operations, errors, duplicates and lost acknowledged reservations. |
| Controls | What stays fixed or is accounted for. | Resources, request mix, data size, duration, cache policy and client location. |
| Repetition | How you distinguish effects from noise. | Independently prepared runs per condition, with varied execution order. |
| Limitations | What the evidence cannot establish. | One VM, a particular workload, shared resources and a finite observation window. |

Define success before collecting comparison data. Choose targets that make sense for your application. If the hypothesis is not supported, report that and investigate why. A careful negative result can demonstrate strong understanding.

The [NIST experimental design handbook](https://www.itl.nist.gov/div898/handbook/pri/section3/pri3.htm) introduces objectives, factors, designs and confounding. A controlled baseline comparison is usually easier to defend than changing many things at once. If several factors vary, design the comparison to distinguish their effects.

## What Is a Test Harness?

A **test harness** is the surrounding software that prepares a system, drives a workload, performs checks and records results. Your application is the **system under test**; the harness controls and observes the experiment around it.

A unit-test harness supplies inputs and fixtures and collects assertions. An advanced application harness coordinates a deployed system, repeatable workloads, optional timed faults, measurements, independent trials, analysis and cleanup.

```text
Scenario configuration + code/image identity
                    |
              Experiment runner
                    |
       Prepare data -> readiness -> warm up
                    |
       Workload + scheduled fault (if studied)
                    |
              Deployed application
                    |
       Timings + outcomes + correctness checks
                    |
       Raw data -> analysis -> figures and conclusions
                    |
              Cleanup / restore
```

Combine existing tools if appropriate: k6 or Locust, kubectl, a data-seeding script and Python analysis. You do not need to write a new HTTP load generator. **Coordination and reproducible evidence make the harness useful**, not the number of tools.

An advanced harness should provide:

- A documented entry point and named scenario configuration.
- Recorded commit, image identity, deployment settings, tool versions and resources.
- Reproducible data preparation, readiness checks and a stated warm-up policy.
- A realistic workload: request mix, user/record distribution and seed where applicable.
- A precise fault schedule when studying failures, with target and failure mechanism.
- Measurements of outcomes and correctness, not just HTTP success codes.
- Independent repetitions, run IDs and start/end times.
- Time limits, resource bounds, an abort condition and cleanup even after failure.
- Raw machine-readable outputs and analysis that regenerates tables and plots.

A possible layout is:

```text
experiments/
  README.md              Setup, reproduction and limitations
  scenarios/             Baseline, treatment, workload and fault settings
  runner/                Preparation, repetitions and cleanup
  workloads/             Load scenarios and correctness checks
  analysis/              Scripts that generate figures from saved data
  results/<run-id>/       Metadata and raw measurements
Report/
  evaluation/            Method, results and interpretation
```

This is illustrative, not a supplied runnable harness. Adapt it to your repository. Exclude credentials, tokens and real personal data from saved outputs.

## Experiment A: Load, Capacity and Scalability

**Question:** what limits the booking application, and does a second API replica improve it?

1. Define realistic operations, such as authenticated reads and reservation attempts. Seed enough distinct data to avoid measuring only one cached record or a permanently conflicting write.
2. Establish a one-replica baseline. Record the database, image digest, resource settings, dataset and generator location.
3. Choose offered load levels within allocated resources, from light load to the region where performance degrades.
4. Compare two replicas under the same workload and duration. State whether total CPU is held constant or each replica receives the same CPU allocation: these answer different questions.
5. Repeat independently. Reset or deliberately preserve state according to your policy. Apply equal warm-up and alternate or randomize execution order to reduce time-related effects.
6. Analyze where successful throughput stops increasing, tail latency grows or errors appear. Connect the effect to application and resource evidence.

| Measurement | Why it matters |
| --- | --- |
| Offered rate and achieved completion rate | Distinguishes demand from useful completed work. |
| Errors, timeouts and dropped work | Prevents rejected work from making a system look deceptively fast. |
| p50, p95 and, with enough samples, p99 latency | Shows typical and tail times; report units and measurement window. |
| Correctness checks | Fast wrong answers, duplicate bookings or lost acknowledged writes are failures. |
| Relevant resource use | Helps identify application, database, network or generator limits. |

Explain your load model. An **open** model schedules arrivals independently of response completion; a **closed** model has a set of users waiting before starting subsequent work. Slow responses can reduce a closed model's offered rate. With an open model, record whether the generator maintained its target and whether work was dropped. [The k6 documentation explains the distinction](https://grafana.com/docs/k6/latest/using-k6/scenarios/concepts/open-vs-closed/).

Where possible, use a generator separate from the application VM. If resources are shared, document the confounder and generator limits. Reaching the generator's CPU ceiling is not evidence of maximum application capacity.

## Experiment B: Resilience and High Availability

**Question:** during a defined failure, does the application keep completing useful operations, and how quickly does it recover?

**High availability** means continuing useful service despite a stated class of failures. **Recovery** restores service after disruption. A Pod restarting does not by itself establish uninterrupted availability.

1. Choose a specific failure, such as loss of one stateless API Pod. State whether it is graceful termination, abrupt failure or something else.
2. Maintain a realistic workload before, during and after the fault. Include a no-fault control.
3. Compare a baseline with a resilience change, such as one versus two ready replicas, under a defined resource policy.
4. Record the injection time and measure from an external client's view. Keep traffic running through the disruption.
5. Define recovery beforehand: for example, your success and latency objective sustained for a specified interval.
6. Check duplicate operations, missing acknowledged writes and other violated invariants. A retry hiding an error while duplicating a booking is not correct recovery.
7. Repeat, restore a known state and report variability and limitations.

Useful outputs include success rate over time, timeouts, latency around the fault, time to sustained recovery and integrity checks. If reporting request-based availability, specify its denominator and window, for example successful intended operations divided by attempted operations during the interval. Define how retries count. A short experiment does not establish annual availability.

### Name the Failure Boundary

| What fails? | What the experiment investigates |
| --- | --- |
| Process or Pod | Application behavior and replacement under that particular failure. |
| Dependency | Timeouts, retry limits, degraded functionality and consistency. |
| Node or VM | Needs independent resources for surviving instances and dependencies. |
| Database, ingress or storage | Reveals remaining single points of failure despite API replication. |

The course cluster normally occupies **one VM**. Two Pods on it do not establish availability against VM loss. Report Pod-level resilience honestly, or choose another rigorous evaluation. Node/VM-level HA experiments need an appropriate environment and a design for storage, database, ingress and control plane as well as the application.

Target only your group's intended experimental workloads. Define limits and cleanup, and keep measurements available when the target fails. Do not destroy the shared cluster, interrupt other groups or repeatedly recreate public certificates as a fault mechanism.

## Other Evaluation Questions

- **Offline support:** compare a synchronization strategy with a baseline; measure convergence, conflicts and correctness under reproducible disconnects.
- **Personalization:** compare a recommendation method with a simple baseline using a justified dataset, quality metric, split and leakage controls; measure cost or latency where relevant.
- **Real-time communication:** compare client counts or interruptions; measure update delay, missing updates and recovery correctness.
- **Advanced testing:** quantitatively evaluate fault detection or application behavior with meaningful end-to-end and failure scenarios. The supplied option includes at least 70% coverage, substantial edge/failure cases, and automation across test environments. Coverage alone is not the experiment.

All routes still build on Grade 4's quality and advanced feature. Evaluate the actual application rather than unrelated tools on a toy task.

## Repetition, Uncertainty and Honest Analysis

Three to five independent trials per condition is a useful starting point, **not a fixed course rule or proof of reliability**. Justify enough repetitions for the observed variability. A million requests in one run are not a million independent repetitions of the treatment.

Show per-run values and a suitable summary of variation. Use confidence intervals only with an explained method and appropriate assumptions; correlated request samples should not imply false certainty. Preserve failed trials. If excluding an instrument failure, state the exclusion rule and retain the raw record.

Label axes and units. Compare equivalent workloads. Lower latency among successful requests may not be an improvement if many more requests fail. An unchanged result may reveal a database bottleneck rather than an API limitation.

## Grade 5 Submission and Demonstration

Include the following in the `Report/` folder or `Report` repository and link the experiment code:

1. Application question, hypothesis and motivation.
2. Setup and architecture, including resources and failure boundaries.
3. Baseline, treatment, controls, workload, dataset and repetitions.
4. Documented harness entry point, versions and scenario configuration.
5. Raw data, run metadata and reproducible analysis with labelled figures.
6. Results, variation, correctness checks and explained bottlenecks or failure behavior.
7. Limitations, threats to validity and a conclusion bounded by the evidence.

At the oral exam, explain why the comparison is fair, what the harness does, what measurements mean and what alternative explanations exist. Be ready to demonstrate a manageable scenario if requested, with full saved results available rather than relying on a long experiment finishing during the examination.

Related material: [Tutorial 10](./README.md) for tests and CI, [Tutorial 5](../05-microservices-and-k8s/README.md) for controller behavior, [Tutorial 4b](../04b-architectures/README.md) for architecture tradeoffs and [optional Tutorial 15](../advanced/15-monitoring/README.md) for measurement tools. A monitoring stack is not a separate numbered pass requirement.
