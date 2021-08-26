# A Demo of EEG Workload

The object is to simulate the Workload of a EEG Device.

## Doing what?

A TCP linked server and client system has been established.

-   The server send simulated EEG epochs every 30 milliseconds in a package.
    Each package has 100 channels and 40 times, which constitutes a 100 x 40 matrix in float.
    To make it serial, the flatten method is used to generate an array.
    Then the matrix is flatten and packed using

    ```python
      # The variable [arr] refers the input matrix
      struct.pack('=%sf' % arr.size, *arr.flatten('F'))
    ```

    Additionally, to identify every package,
    the server put the package ID at the `37th` (starts from `0th`) element of the array.
    The ID is started from `0` at step of `1`.

-   The client receives the packages from established TCP channel,
    which is too simple to be mentioned.
    And the client also report what it got at every package is received.
    Specifically, it will report the ID (the `33th` element) and the `34th` element to make sure the translation is working properly.

## Any results?

The outcome is just fine.

-   The system is working just fine;
-   It consumes about `4-5` Mbps network on translation;
-   No package is lost or swapped during translation neither.

## One more thing?

When you are using windows PC for the server,
you need to tell your firewall to allow the given port for the remote client connection.

> More Importantly, you should restart your machine after you do so.
> Basically, you should restart your machine at anytime you find anything abnormal on your machine.
> It can save you from everything bad.
