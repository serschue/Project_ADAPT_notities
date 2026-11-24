# Guidance 

## Why would we use guidance and not filter afterwards?

Guidance is only cheaper when the relative improvement in success rate exceeds the relative increase in computational cost. 

- \(C\) = cost of unconditional generation
- \(G\) = additional guidance cost per sample
- \(p\) = success probability without guidance
- \(q\) = success probability with guidance
  Guidance is cheaper when:

$$
\frac{C+G}{q}<\frac{C}{p}
$$

Rearranging:
$$
\boxed{\frac{q}{p}>1+\frac{G}{C}}
$$



Example: 

|                                      | Generate + select | Classifier guidance |
| ------------------------------------ | ----------------- | ------------------- |
| Cost per sample                      | 1 min             | 1.5 min             |
| Success rate                         | 5%                | 30%                 |
| Samples for 100 successes (expected) | 2,000             | 334                 |
| Total generation cost                | 2,000 min         | 501 min             |

![image-20261019135313942](/home/sarah/.config/Typora/typora-user-images/image-20261019135313942.png)
