![Quality](https://github.com/SQR-Project/University-Dating/actions/workflows/quality.yaml/badge.svg)

![Deploy](https://github.com/SQR-Project/University-Dating/actions/workflows/deploy.yaml/badge.svg)

# University-Dating

## Mutation Tests

Result:

`200/200  🎉 176  ⏰ 0  🤔 0  🙁 23  🔇 0`

## Tests Coverage

```
Name                                      Stmts   Miss Branch BrPart  Cover
---------------------------------------------------------------------------
app/main.py                                  17      2      2      0    89%
app/src/controllers/auth.py                  20      0      8      0   100%
app/src/controllers/matching.py              13      0      4      0   100%
app/src/controllers/profile.py               17      0      6      0   100%
app/src/controllers/status.py                 7      0      2      0   100%
app/src/dal/database.py                      46      0      0      0   100%
app/src/enums/interests_enum.py               7      0      0      0   100%
app/src/models/auth.py                        7      0      0      0   100%
app/src/models/like.py                        5      0      0      0   100%
app/src/models/profile.py                    10      0      0      0   100%
app/src/models/response.py                    3      0      0      0   100%
app/src/services/auth_service.py             83      0     12      0   100%
app/src/services/like_service.py             23      0      0      0   100%
app/src/services/profile_service.py          26      0      2      0   100%
app/src/ui/login.py                          85      0     10      0   100%
app/src/ui/matching.py                       53      5     10      1    90%
app/src/validators/email_validator.py         9      0      2      0   100%
app/src/validators/profile_validator.py      13      0      4      0   100%
app/ui_app.py                                17     17      6      0     0%
---------------------------------------------------------------------------
TOTAL                                       461     24     68      1    94%
```

## Performance testing

We have failures for 'create' and 'delete' routes because it is impossible to run them one by one using locust

![Performance testing](/images/performance.png)