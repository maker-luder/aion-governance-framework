package aion.interop_test

import data.aion.interop

test_policy_has_fail_closed_default if {
  interop.allow == false with input as {}
}
